class BundleInfo:

    class GameInfo:
        def __init__(self):
            self.app_id = None
            self.name = None
            self.total_reviews = None
            self.total_positive = None
            self.price = None
            self.genres = []

    def __init__(self):
        self.bundle_id = None
        self.games: list[BundleInfo.GameInfo] = []
