@router.get("/{dataset_id}/profile")
def get_dataset_profile(
    dataset_id: str,
    db: Session = Depends(get_db)
):
    dataset = DatasetRepository.get_by_id(db, dataset_id)

    if dataset is None:
        raise HTTPException(
            status_code=404,
            detail="Dataset not found."
        )

    file_path = Path(settings.UPLOAD_DIR) / dataset.stored_filename

    df = DatasetService.read_dataset(
        file_path=file_path,
        extension=dataset.extension
    )

    profile = DatasetService.generate_profile(df)

    return {
        "dataset_id": dataset.dataset_id,
        "filename": dataset.original_filename,
        "profile": profile
    }