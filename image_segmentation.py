## Apply image seg and detect the position of face
import fitz
import traceback
import os
import matplotlib.pyplot as plt
from PIL import Image
import io

class PDFImageDetector:
    def __init__(self):
        print("PDFImageDetector initialized")

    def detect_images(self, pdf_path, save_path=None, plot_images=False):
        try:
            doc = fitz.open(pdf_path)
            images = []

            for page_num, page in enumerate(doc, start=1):
                image_list = page.get_images(full=True)
                
                for img_index, img in enumerate(image_list, start=1):
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    
                    image_info = {
                        "page_num": page_num,
                        "image_index": img_index,
                        "width": base_image["width"],
                        "height": base_image["height"],
                        "position": self.get_image_position(page, img),
                        "image_data": image_bytes
                    }
                    images.append(image_info)

                    if save_path:
                        self.save_image(image_info, save_path)

            doc.close()

            if plot_images:
                self.plot_images(images)

            return images
        except Exception as e:
            print(f"An error occurred while processing the PDF: {e}")
            print(traceback.format_exc())
            return []

    def get_image_position(self, page, img):
        try:
            xref = img[0]
            for item in page.get_image_info():
                if 'xref' in item and item["xref"] == xref:
                    return item.get("bbox")
                elif 'number' in item and item["number"] == xref:
                    return item.get("bbox")
            return None
        except Exception as e:
            print(f"Error getting image position: {e}")
            return None

    def save_image(self, image_info, save_path):
        try:
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            
            filename = f"page_{image_info['page_num']}_img_{image_info['image_index']}.png"
            filepath = os.path.join(save_path, filename)
            
            image = Image.open(io.BytesIO(image_info['image_data']))
            image.save(filepath)
            print(f"Saved image: {filepath}")
        except Exception as e:
            print(f"Error saving image: {e}")

    def plot_images(self, images):
        for img in images:
            plt.figure(figsize=(8, 8))
            image = Image.open(io.BytesIO(img['image_data']))
            plt.imshow(image)
            plt.title(f"Page {img['page_num']}, Image {img['image_index']}")
            plt.axis('off')
            plt.show()

    def print_image_info(self, images):
        if not images:
            print("No images found or error occurred during processing.")
            return
        
        for img in images:
            print(f"第 {img['page_num']} 页, 图片 {img['image_index']}:")
            print(f"  尺寸: {img['width']} x {img['height']}")
            if img['position']:
                print(f"  位置: 左上({img['position'][0]:.2f}, {img['position'][1]:.2f}), "
                      f"右下({img['position'][2]:.2f}, {img['position'][3]:.2f})")
            else:
                print("  位置: 未能获取")
            print()

if __name__ == "__main__":
    detector = PDFImageDetector()
    save_path = "./images"
    images = detector.detect_images("中文履歷.pdf", save_path=save_path, plot_images=True)
    detector.print_image_info(images)   

