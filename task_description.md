Description:
The task is to use the Encord SDK to upload labels to a project.
Assume this export format comes from a customer's internal system.

Once you are signed up to the platform after receiving an email invite, you should have access to a project 'Label Import Challenge - Your Name'.
You will need to write a Python script to convert the customer's export in order to upload labels programmatically to the videos in this project.

Please spend a maximum of 2 hours on this task.
Prioritise uploading the bounding boxes and then the filling of the box attributes. If you don't have time to figure out how to fill the box attributes, please write a few sentences describing how you would go about this and what attempts you made.

Please ask questions by email if you get stuck after searching through the docs. We work as a team!

Hints:
- Here is a link that explains how to authenticate using the SDK https://docs.encord.com/sdk-documentation/general-sdk/authentication-sdk
- You should refer to this part of the documentation for uploading labels, where you can find partially worked examples: https://docs.encord.com/sdk-documentation/sdk-labels/sdk-working-with-labels
- The origin of the coordinate system is the top left corner of the frame. Encord uses normalised x,y coordinates which can take on values from 0 to 1.
- Encord's format for bounding boxes is (top_left_x, top_left_y, width, height) (see docs https://docs.encord.com/sdk-documentation/sdk-labels/sdk-working-with-labels#creating-reading-object-instances)
- Individual instances of an object are identified by their annotation_id. In Encord, a single instance can have annotations spanning multiple frames. Ideally we would like annotations with the same annotation_id to live under the same object instance.
- An example of how to answer object attributes can be found in the docs: https://docs.encord.com/sdk-documentation/sdk-labels/sdk-working-with-labels#answering-object-instance-attributes
