from app.services.cleaning_service import CleaningService
from app.services.validation_service import ValidationService
from app.services.transformation_service import TransformationService
from app.services.dataset_service import DatasetService

from app.core.config import settings
from pathlib import Path


class PipelineService:

    @staticmethod
    def get_operation_order(steps):

        return sorted(
            steps,
            key=lambda step: step.step_order
        )

    @staticmethod
    def normalize_operation(operation):

        return operation.strip().upper()

    @staticmethod
    def get_service(operation):

        operation = PipelineService.normalize_operation(operation)

        if operation == "CLEAN":
            return CleaningService

        elif operation == "VALIDATE":
            return ValidationService

        elif operation == "TRANSFORM":
            return TransformationService

        elif operation == "PROFILE":
            return DatasetService

        else:
            raise ValueError(
                f"Unsupported pipeline operation: {operation}"
            )

    @staticmethod
    def execute_steps(steps):

        ordered_steps = PipelineService.get_operation_order(steps)

        results = []

        for step in ordered_steps:

            operation = PipelineService.normalize_operation(
                step.operation
            )

            service = PipelineService.get_service(operation)

            results.append({
                "step_order": step.step_order,
                "operation": operation,
                "service": service.__name__
            })

        return results

    @staticmethod
    def execute_clean(df, dataset):

        df, cleaning_info = CleaningService.clean_dataset(df)

        cleaned_file = CleaningService.save_cleaned_dataset(
            df,
            dataset.original_filename
        )

        return df, {
            "operation": "CLEAN",
            "cleaning_info": cleaning_info,
            "cleaned_file": str(cleaned_file)
        }


    
    @staticmethod
    def execute_validate(df):

        validation = ValidationService.validate_dataset(df)

        return {
            "operation": "VALIDATE",
            "validation": validation
        }

    @staticmethod
    def execute_transform(df, dataset):

        df, transformation_info = TransformationService.transform_dataset(df)

        transformed_file = TransformationService.save_transformed_dataset(
            df,
            dataset.original_filename
        )

        return df, {
            "operation": "TRANSFORM",
            "transformation_info": transformation_info,
            "transformed_file": str(transformed_file)
        }
    
    @staticmethod
    def execute_profile(df, dataset):

        profile = DatasetService.generate_profile(df)

        profile_file = DatasetService.save_profile_report(
            profile,
            dataset.original_filename
        )

        return {
            "operation": "PROFILE",
            "profile": profile,
            "profile_file": str(profile_file)
        }

    @staticmethod
    def load_dataset(dataset):

        file_path = Path(settings.UPLOAD_DIR) / dataset.stored_filename

        return DatasetService.read_dataset(
            file_path=file_path,
            extension=dataset.extension
        )