import requests
class Description_Generator:
    def __init__(self,debug_mode=False):
        self.debug_mode=debug_mode
        key_values = open("key.txt", "r").read().splitlines()
        self.subscription_key=key_values[0]
        vision_base_url = "https://eastus.api.cognitive.microsoft.com/vision/v2.0/"
        self.analyze_url = vision_base_url + "analyze"

    '''
    Get description and related information about the given image
    :param image_data: given image in bytes
    :returns: returned result in json format
    '''
    def analyze_image(self,image_data,string_only):
        # Set image_path to the local path of an image that you want to analyze.
        image_path = "testimg_tiny.jpg"

        # Read the image into a byte array
        #image_data = open(image_path, "rb").read()
        headers = {'Ocp-Apim-Subscription-Key': self.subscription_key,
                   'Content-Type': 'application/octet-stream'}
        params = {'visualFeatures': 'Categories,Description,Color'}
        response = requests.post(
            self.analyze_url, headers=headers, params=params, data=image_data)
        response.raise_for_status()
        # sample output
        #{'categories': [{'name': 'people_many', 'score': 0.7578125, 'detail': {'celebrities': []}}], 'color': {'dominantColorForeground': 'Black', 'dominantColorBackground': 'Black', 'dominantColors': ['Black', 'Brown'], 'accentColor': '784137', 'isBwImg': False}, 'description': {'tags': ['person', 'indoor', 'ceiling', 'people', 'group', 'table', 'sitting', 'laptop', 'room', 'computer', 'large', 'crowd', 'man', 'full', 'food', 'watching', 'front', 'filled', 'playing', 'screen', 'standing', 'video', 'restaurant', 'eating', 'pizza', 'game', 'wii'], 'captions': [{'text': 'a group of people sitting at a table in front of a crowd', 'confidence': 0.957287532624088}]}, 'requestId': 'c83c4203-07e2-4dd2-ae97-d7fcd70dfbfd', 'metadata': {'width': 3264, 'height': 2448, 'format': 'Jpeg'}}
        analysis = response.json()
        if string_only:
            if 'description' in analysis and 'captions' in analysis.get('description'):
                captions_result=analysis.get('description').get('captions')
                if len(captions_result)>0:
                    return captions_result[0].get('text')

            return 'No obvious changes'
        else:
            if self.debug_mode:
                print(analysis)
            return analysis
