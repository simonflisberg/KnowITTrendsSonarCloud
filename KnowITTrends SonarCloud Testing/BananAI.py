from google import genai

class BananAI:
    def __init__(self):
        self._client = genai.Client(api_key="AIzaSyAS3P0o0JY8mmkdE-K_IVnb-z1IO5xzWrw")
        self._model = "gemini-2.0-flash"
    
    def SendRequest(self, 
                    query: str):
        """
        Queries the AI-model and returns the generated answer.

        Args:
            query (str): The query to promt the AI.
        
        Returns:
            out (str): String containing the AI generated answer to the query.
        """
        
        try_c = 0

        while try_c <= 2:
            try:
                response = self._client.models.generate_content(
                model="gemini-2.0-flash", contents=query
                )
                try_c = 3
            except Exception as e:
                print(f"Error querying Gemini: {e}. Trying again, I will try three times.")
                try_c += 1

        if response.candidates and len(response.candidates) > 0:
            candidate = response.candidates[0]
            text = candidate.content.parts[0].text
            return text
        else:
            return "No candidate returned."
    
    def GetCrazyBananasPrediction(self, datapoints: list):
        """
        Cooks up a crazy bananas prediction
        Args:
            datapoints (list): A timeseries of datapoints including data and price

        Returns:
            out (json): A totaly crazy bananas prediction
        """
        query = f"Only include the json, no other text or signs, the message should be formatted as a json string, remove all formatting stuff, it should only contain original json characters and does not need to be readable so that i can import it in python with no problems. I dont want you to use \n or ` or other stuff like that. DONT INCLUDE ```json\n. or other stuff like that You can include a description including a disclaimer (This is not financial advide) in the json (call the prediction prediction and description decsription). All parts of the predictions should be based on the series of data available. Make a continous prediction of the following data series but insead of trend include optimistic and pesimistic predictions based on the data also include a baseline prediction: {datapoints}"

        return self.SendRequest(query=query)

if __name__ == "__main__":
    ai = BananAI()
    #print(ai.SendRequest(query="What is a banana?"))
    data = [{'date': '2015-01-01', 'value': 47.56, 'trend': 41.51}, {'date': '2015-02-01', 'value': 50.86, 'trend': 41.86}, {'date': '2015-03-01', 'value': 47.78, 'trend': 42.17}, {'date': '2015-04-01', 'value': 54.38, 'trend': 42.52}, {'date': '2015-05-01', 'value': 59.39, 'trend': 42.86}, {'date': '2015-06-01', 'value': 59.83, 'trend': 43.21}, {'date': '2015-07-01', 'value': 51.2, 'trend': 43.55}, {'date': '2015-08-01', 'value': 42.91, 'trend': 43.9}, {'date': '2015-09-01', 'value': 45.51, 'trend': 44.25}, {'date': '2015-10-01', 'value': 46.27, 'trend': 44.59}, {'date': '2015-11-01', 'value': 42.59, 'trend': 44.94}, {'date': '2015-12-01', 'value': 37.4, 'trend': 45.28}, {'date': '2016-01-01', 'value': 31.78, 'trend': 45.63}, {'date': '2016-02-01', 'value': 30.38, 'trend': 45.98}, {'date': '2016-03-01', 'value': 37.9, 'trend': 46.31}, {'date': '2016-04-01', 'value': 41.03, 'trend': 46.66}, {'date': '2016-05-01', 'value': 46.84, 'trend': 46.99}, {'date': '2016-06-01', 'value': 48.79, 'trend': 47.34}, {'date': '2016-07-01', 'value': 44.9, 'trend': 47.68}, {'date': '2016-08-01', 'value': 44.75, 'trend': 48.03}, {'date': '2016-09-01', 'value': 45.2, 'trend': 48.38}, {'date': '2016-10-01', 'value': 49.81, 'trend': 48.72}, {'date': '2016-11-01', 'value': 45.47, 'trend': 49.07}, {'date': '2016-12-01', 'value': 52.05, 'trend': 49.41}, {'date': '2017-01-01', 'value': 52.56, 'trend': 49.76}, {'date': '2017-02-01', 'value': 53.45, 'trend': 50.11}, {'date': '2017-03-01', 'value': 49.36, 'trend': 50.43}, {'date': '2017-04-01', 'value': 51.17, 'trend': 50.78}, {'date': '2017-05-01', 'value': 48.56, 'trend': 51.12}, {'date': '2017-06-01', 'value': 45.19, 'trend': 51.47}, {'date': '2017-07-01', 'value': 46.58, 'trend': 51.8}, {'date': '2017-08-01', 'value': 48.05, 'trend': 52.15}, {'date': '2017-09-01', 'value': 49.74, 'trend': 52.5}, {'date': '2017-10-01', 'value': 51.57, 'trend': 52.84}, {'date': '2017-11-01', 'value': 56.74, 'trend': 53.19}, {'date': '2017-12-01', 'value': 57.92, 'trend': 53.53}, {'date': '2018-01-01', 'value': 63.58, 'trend': 53.88}, {'date': '2018-02-01', 'value': 62.23, 'trend': 54.23}, {'date': '2018-03-01', 'value': 62.83, 'trend': 54.55}, {'date': '2018-04-01', 'value': 66.31, 'trend': 54.9}, {'date': '2018-05-01', 'value': 69.9, 'trend': 55.24}, {'date': '2018-06-01', 'value': 67.88, 'trend': 55.59}, {'date': '2018-07-01', 'value': 71.07, 'trend': 55.92}, {'date': '2018-08-01', 'value': 67.93, 'trend': 56.27}, {'date': '2018-09-01', 'value': 70.19, 'trend': 56.62}, {'date': '2018-10-01', 'value': 70.75, 'trend': 56.96}, {'date': '2018-11-01', 'value': 56.19, 'trend': 57.31}, {'date': '2018-12-01', 'value': 48.92, 'trend': 57.65}, {'date': '2019-01-01', 'value': 51.23, 'trend': 58.0}, {'date': '2019-02-01', 'value': 55.0, 'trend': 58.35}, {'date': '2019-03-01', 'value': 58.17, 'trend': 58.67}, {'date': '2019-04-01', 'value': 63.87, 'trend': 59.02}, {'date': '2019-05-01', 'value': 60.74, 'trend': 59.36}, {'date': '2019-06-01', 'value': 54.67, 'trend': 59.71}, {'date': '2019-07-01', 'value': 57.38, 'trend': 60.05}, {'date': '2019-08-01', 'value': 54.83, 'trend': 60.4}, {'date': '2019-09-01', 'value': 56.86, 'trend': 60.75}, {'date': '2019-10-01', 'value': 53.96, 'trend': 61.08}, {'date': '2019-11-01', 'value': 56.68, 'trend': 61.43}, {'date': '2019-12-01', 'value': 59.87, 'trend': 61.77}, {'date': '2020-01-01', 'value': 57.72, 'trend': 62.12}, {'date': '2020-02-01', 'value': 50.61, 'trend': 62.47}, {'date': '2020-03-01', 'value': 29.32, 'trend': 62.8}, {'date': '2020-04-01', 'value': 16.98, 'trend': 63.15}, {'date': '2020-05-01', 'value': 28.78, 'trend': 63.49}, {'date': '2020-06-01', 'value': 38.31, 'trend': 63.84}, {'date': '2020-07-01', 'value': 40.72, 'trend': 64.18}, {'date': '2020-08-01', 'value': 42.37, 'trend': 64.53}, {'date': '2020-09-01', 'value': 39.6, 'trend': 64.88}, {'date': '2020-10-01', 'value': 39.41, 'trend': 65.22}, {'date': '2020-11-01', 'value': 41.39, 'trend': 65.57}, {'date': '2020-12-01', 'value': 47.07, 'trend': 65.91}, {'date': '2021-01-01', 'value': 51.85, 'trend': 66.26}, {'date': '2021-02-01', 'value': 59.23, 'trend': 66.61}, {'date': '2021-03-01', 'value': 62.18, 'trend': 66.92}, {'date': '2021-04-01', 'value': 61.42, 'trend': 67.27}, {'date': '2021-05-01', 'value': 65.16, 'trend': 67.61}, {'date': '2021-06-01', 'value': 71.38, 'trend': 67.96}, {'date': '2021-07-01', 'value': 72.59, 'trend': 68.3}, {'date': '2021-08-01', 'value': 67.87, 'trend': 68.65}, {'date': '2021-09-01', 'value': 71.53, 'trend': 69.0}, {'date': '2021-10-01', 'value': 81.36, 'trend': 69.34}, {'date': '2021-11-01', 'value': 79.1, 'trend': 69.69}, {'date': '2021-12-01', 'value': 71.8, 'trend': 70.03}, {'date': '2022-01-01', 'value': 83.28, 'trend': 70.38}, {'date': '2022-02-01', 'value': 91.61, 'trend': 70.73}, {'date': '2022-03-01', 'value': 108.4, 'trend': 71.04}, {'date': '2022-04-01', 'value': 102.0, 'trend': 71.39}, {'date': '2022-05-01', 'value': 109.7, 'trend': 71.73}, {'date': '2022-06-01', 'value': 114.7, 'trend': 72.08}, {'date': '2022-07-01', 'value': 101.9, 'trend': 72.42}, {'date': '2022-08-01', 'value': 93.69, 'trend': 72.77}, {'date': '2022-09-01', 'value': 84.4, 'trend': 73.12}, {'date': '2022-10-01', 'value': 87.29, 'trend': 73.46}, {'date': '2022-11-01', 'value': 84.08, 'trend': 73.81}, {'date': '2022-12-01', 'value': 76.58, 'trend': 74.15}, {'date': '2023-01-01', 'value': 78.25, 'trend': 74.5}, {'date': '2023-02-01', 'value': 77.03, 'trend': 74.85}, {'date': '2023-03-01', 'value': 73.35, 'trend': 75.16}, {'date': '2023-04-01', 'value': 79.13, 'trend': 75.51}, {'date': '2023-05-01', 'value': 71.67, 'trend': 75.85}, {'date': '2023-06-01', 'value': 70.31, 'trend': 76.2}, {'date': '2023-07-01', 'value': 75.77, 'trend': 76.54}, {'date': '2023-08-01', 'value': 81.37, 'trend': 76.89}, {'date': '2023-09-01', 'value': 89.24, 'trend': 77.24}, {'date': '2023-10-01', 'value': 85.47, 'trend': 77.58}, {'date': '2023-11-01', 'value': 77.58, 'trend': 77.93}, {'date': '2023-12-01', 'value': 72.02, 'trend': 78.27}, {'date': '2024-01-01', 'value': 74.0, 'trend': 78.62}, {'date': '2024-02-01', 'value': 77.36, 'trend': 78.97}, {'date': '2024-03-01', 'value': 81.41, 'trend': 79.3}, {'date': '2024-04-01', 'value': 85.35, 'trend': 79.65}, {'date': '2024-05-01', 'value': 79.96, 'trend': 79.98}, {'date': '2024-06-01', 'value': 79.91, 'trend': 80.33}, {'date': '2024-07-01', 'value': 81.95, 'trend': 80.67}, {'date': '2024-08-01', 'value': 76.68, 'trend': 81.02}, {'date': '2024-09-01', 'value': 70.44, 'trend': 81.37}, {'date': '2024-10-01', 'value': 72.16, 'trend': 81.71}, {'date': '2024-11-01', 'value': 69.94, 'trend': 82.06}, {'date': '2024-12-01', 'value': 70.15, 'trend': 82.4}, {'date': '2025-01-01', 'value': 75.65, 'trend': 82.75}, {'date': '2025-02-01', 'value': 71.54, 'trend': 83.1}]
    print(ai.GetCrazyBananasPrediction(data))