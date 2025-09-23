import asyncio
import base64
import os
from io import BytesIO

import grpc
from concurrent import futures
from datetime import datetime
import pandas as pd
from protos import service_pb2
from protos import service_pb2_grpc
import time
from insights import annual_stats
from kenjaAI import get_esg_report


class EsgReportService(service_pb2_grpc.EsgReportServiceServicer):

    def UploadCSV(self, request, context):
        print("Upload request is running")
        global csv_path, data
        timestamp = datetime.now().astimezone().strftime("%Y%m%d%H%M%S")
        csv_path = f"./csv_dataset" + ".csv"

        with open(csv_path, "wb") as f:
            f.write(request.file_content)

        try:
            data = pd.read_csv(csv_path)
            return service_pb2.UploadCSVResponse(
                status="success",
                message=f"CSV uploaded and saved to {csv_path}"
            )
        except Exception as e:
            print("Error:", e)
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return service_pb2.UploadCSVResponse(status="failed", message="error")


    def GenerateEsgReport(self, request, context):
        print("Generating EsgReport request in gRPC")
        global data, file_path
        csv_path = fr".\csv_dataset.csv"

        if not os.path.exists(csv_path):
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("CSV not found on server. Please check the file name.")
            return service_pb2.GenerateEsgReportResponse(
                esg_report="",
                stats_data=service_pb2.StatsData(
                facility_name="",
                total_annual_emissions=0.0,
                mean_annual_emissions=0.0,
                mean_capture_efficiency=0.0,
                mean_storage_integrity=0.0,
                minimum_capture_efficiency=0.0,
                minimum_storage_integrity=0.0
            )
        )

        data = pd.read_csv(csv_path)

        if data.empty:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("No csv loaded. Use /set_csv/ before anything.")
            return service_pb2.GenerateEsgReportResponse(
                esg_report="",
                stats_data=service_pb2.StatsData(
                    facility_name="",
                    total_annual_emissions=0.0,
                    mean_annual_emissions=0.0,
                    mean_capture_efficiency=0.0,
                    mean_storage_integrity=0.0,
                    minimum_capture_efficiency=0.0,
                    minimum_storage_integrity=0.0,
                    total_captured_tonnes = 0,
                    total_stored_tonnes = 0,
                    date_time = "",
                )
            )

        stats_dict = annual_stats(data, request.facility_name)
        esg_report = asyncio.run(get_esg_report(stats_dict))

        stats = service_pb2.StatsData(
            facility_name=stats_dict["facility_name"],
            total_annual_emissions=stats_dict["total_annual_emissions"],
            mean_annual_emissions=stats_dict["mean_annual_emissions"],
            mean_capture_efficiency=stats_dict["mean_capture_efficiency"],
            mean_storage_integrity=stats_dict["mean_storage_integrity"],
            minimum_capture_efficiency=stats_dict["minimum_capture_efficiency"],
            minimum_storage_integrity=stats_dict["minimum_storage_integrity"],
            total_captured_tonnes = stats_dict["total_captured_tonnes"],
            total_stored_tonnes = stats_dict["total_stored_tonnes"],
            date_time = stats_dict["date_time"],
        )

        return service_pb2.GenerateEsgReportResponse(
            esg_report=esg_report,
            stats_data=stats
        )



def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_EsgReportServiceServicer_to_server(EsgReportService(), server)
    server.add_insecure_port('[::]:50051')
    print("Starting server on port 50051...")
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        print("Stopping server...")
        server.stop(0)

if __name__ == '__main__':
    serve()