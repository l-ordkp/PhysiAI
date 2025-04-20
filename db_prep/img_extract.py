import os
from dotenv import load_dotenv
from llama_parse import LlamaParse
from llama_index.core.schema import ImageDocument
from typing import List
load_dotenv()
llama_key = os.getenv("LLAMA_CLOUD_API_KEY")
parser = LlamaParse(
    api_key=llama_key,
    result_type="markdown",
)

json_objs = parser.get_json_result("/Users/kshitijpal/Desktop/PhysiAI/iesc111.pdf")
json_list = json_objs[0]["pages"]
def get_image_nodes(json_objs: List[dict], download_path: str) -> List[ImageDocument]:
    image_dicts = parser.get_images(json_objs, download_path=download_path)
    return [ImageDocument(image_path=image_dict["path"]) for image_dict in image_dicts]

image_documents = get_image_nodes(json_objs, "/Users/kshitijpal/Desktop/PhysiAI/images")
