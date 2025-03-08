# Import dependencies
from typing import List, Dict
from encord import EncordUserClient
from encord.objects import Object, Option
from encord.objects.coordinates import BoundingBoxCoordinates
from encord.objects.attributes import RadioAttribute
import json

def read_export_file(filepath: str) -> tuple[dict, dict]:
    """Read and parse the export.json file and return annotations and metadata"""
    with open(filepath, 'r') as f:
        data = json.load(f)
        # Create a lookup dictionary that stores lists of metadata entries
        metadata_lookup = {}
        for item in data["annotation_metadata"]:
            annotation_id = item["annotation_id"]
            if annotation_id not in metadata_lookup:
                metadata_lookup[annotation_id] = []
            metadata_lookup[annotation_id].append(item)
        return data, metadata_lookup

def get_video_dimensions(video_meta: List[dict], file_id: str) -> tuple[int, int]:
    """Get width and height for a specific video file"""
    for video in video_meta:
        if video["file_id"] == file_id:
            return video["width"], video["height"]
    raise ValueError(f"Video metadata not found for file_id: {file_id}")

def convert_coordinates(annotation: dict, width: int, height: int) -> BoundingBoxCoordinates:
    """Convert annotation coordinates to normalized BoundingBoxCoordinates"""
    coords = annotation["coordinates"]
    
    # Calculate bounding box dimensions from corners
    min_x = min(point["x"] for point in coords)
    min_y = min(point["y"] for point in coords)
    max_x = max(point["x"] for point in coords)
    max_y = max(point["y"] for point in coords)
    
    # Normalize coordinates
    return BoundingBoxCoordinates(
        top_left_x=min_x / width,
        top_left_y=min_y / height,
        width=(max_x - min_x) / width,
        height=(max_y - min_y) / height
    )

def main():
    # Initialize client
    user_client = EncordUserClient.create_with_ssh_private_key(
        ssh_private_key_path="ssh-private-key.ed25519"
    )
    
    # Get project and label rows
    PROJECT_HASH = "0523e87c-ba40-4eb7-8cf6-43a3369bc6dc"  # Replace with your project hash
    project = user_client.get_project(PROJECT_HASH)
    label_rows = project.list_label_rows_v2()
    
    # Read export data
    export_data, metadata_lookup = read_export_file("export.json")
    video_meta = export_data["video_meta"]
    annotations = export_data["annotations"]
    
    # Create a mapping of file_id to label_row
    file_to_label_row = {}
    for label_row in label_rows:
        label_row.initialise_labels()
        # Assuming the label row title or data contains the file_id
        # You might need to adjust this based on how files are matched to label rows
        print(f"Discovered label row: {label_row.data_title}")

        normalized_label = label_row.data_title.split(".")[0]        
        file_to_label_row[normalized_label] = label_row
    
    # Group annotations by file_id and annotation_id
    file_instances: Dict[str, Dict[str, Dict[int, BoundingBoxCoordinates]]] = {}
    
    for annotation in annotations:
        file_id = annotation["file_id"]
        annotation_id = annotation["annotation_id"]
        frame_number = int(annotation["frame"])
        
        # Get video dimensions for this file
        width, height = get_video_dimensions(video_meta, file_id)
        coordinates = convert_coordinates(annotation, width, height)
        
        if file_id not in file_instances:
            file_instances[file_id] = {}
        if annotation_id not in file_instances[file_id]:
            file_instances[file_id][annotation_id] = {}
            
        file_instances[file_id][annotation_id][frame_number] = coordinates
    
    # Process each file's annotations
    for file_id, instances in file_instances.items():
        if file_id not in file_to_label_row:
            print(f"Warning: No label row found for file '{file_id}'")
            continue
            
        label_row = file_to_label_row[file_id]
        ontology_structure = label_row.ontology_structure
        person_object = ontology_structure.get_child_by_title(
            title="Person", type_=Object
        )
        
        # Get the attribute objects from ontology
        walking_speed_attr = ontology_structure.get_child_by_title(
            title="Walking Speed", type_=RadioAttribute
        )
        shoes_attr = ontology_structure.get_child_by_title(
            title="Shoes", type_=RadioAttribute
        )
        clothing_attr = ontology_structure.get_child_by_title(
            title="Clothing", type_=RadioAttribute
        )
        
        # Create and add object instances for this file
        for annotation_id, frames_coords in instances.items():
            object_instance = person_object.create_instance()
            
            # Add coordinates for each frame
            for frame_number, coordinates in frames_coords.items():
                object_instance.set_for_frames(
                    coordinates=coordinates,
                    frames=frame_number
                )
            
            # Add metadata if it exists for this annotation_id
            if annotation_id in metadata_lookup:
                for metadata in metadata_lookup[annotation_id]:
                    # Set the appropriate attribute based on the question
                    if metadata["question"] == "Walking Speed":
                        object_instance.set_answer(
                            answer=walking_speed_attr.get_child_by_title(metadata["answer"], type_=Option)
                        )
                    elif metadata["question"] == "Shoes":
                        object_instance.set_answer(
                            answer=shoes_attr.get_child_by_title(metadata["answer"], type_=Option)
                        )
                    elif metadata["question"] == "Clothing":
                        object_instance.set_answer(
                            answer=clothing_attr.get_child_by_title(metadata["answer"], type_=Option)
                        )
            
            label_row.add_object_instance(object_instance)
        
        # Save changes for this label row
        label_row.save()
        print(f"Successfully uploaded annotations for {file_id}")

if __name__ == "__main__":
    main()

