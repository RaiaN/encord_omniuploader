# Import necessary modules from the Encord SDK
from encord import EncordClient

# Authenticate with Encord
client = EncordClient(api_key="YOUR_API_KEY")


def main():
    # Prepare your label data
    # Example label data format
    labels = [
        {
            "annotation_id": "unique_id_1",
            "frame_number": 1,
            "bounding_box": (0.1, 0.2, 0.3, 0.4),  # Normalized coordinates
            "attributes": {"attribute_key": "attribute_value"}
        },
        # Add more labels as needed
    ]

    # Upload labels
    for label in labels:
        client.upload_label(
            project_id="YOUR_PROJECT_ID",
            label_data=label
        )


if __name__ == "__main__":
    main()

