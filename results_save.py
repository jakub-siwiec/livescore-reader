from datetime import datetime
import pickle


class ResultsSave:
    def __init__(self, content=[], file_title=None):
        """Saving or loading the content to from the file. It can save to pickle, txt and json file and load a variable from a pickle file.

        Args:
            content (list, optional): It is the content to save in the file. Defaults to [].
            file_title (string, optional): This is the file title used for file naming. If None then the file will be in the format resultsYYYYmmddHHMMss, eg. results20201121200421 means the file was saved on the 21st of November 2020 at 20:04:21. Defaults to None.
        """
        self.content = content
        if file_title == None:
            self.file_title = "results" + datetime.now().strftime("%Y%m%d%H%M%S")
        else:
            self.file_title = file_title

    def export_pickle(self):
        """Export variable into a pickle file.
        """
        pickle.dump(self.content, open(self.file_title, "wb"))

    def load_pickle(self):
        """Load pickle file.

        Returns:
            undefined: The content read in a pickle file.
        """
        content = pickle.load(open(self.file_title, "rb"))
        self.content = content
        return self.content

    def export_txt(self):
        """Export string into a txt file. Content must be of string or json type.

        Raises:
            TypeError: If it is not string it cannot export the file.
        """
        if isinstance(self.content, str):
            f = open(self.file_title + ".txt", "w")
            f.write(self.content)
            f.close()
        else:
            raise TypeError("The type of the content in .txt must be a string")

    def export_json(self):
        """Export string into a txt file. Content must be of a proper string or json type.

        Raises:
            TypeError: If it is not string it cannot export the file.
        """
        if isinstance(self.content, str):
            f = open(self.file_title + ".json", "w")
            f.write(self.content)
            f.close()
        else:
            raise TypeError("The type of the content in .txt must be a string")
