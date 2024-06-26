import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class FuzzyCMeans:
    def __init__(
        self,
        n_clusters=5,
        m=3,
        max_iter=100,
        tolerance=0.00001,
        random_state=42,
        init=None,
    ):
        """
        Initializes the Fuzzy C-Means clustering algorithm.

        Args:
            n_clusters (int): The number of clusters to form.
            m (float): The fuzziness parameter (m > 1). Controls the degree of fuzziness in cluster assignments.
            max_iter (int): The maximum number of iterations.
            tolerance (float): Convergence threshold based on changes in the membership matrix.
            random_state (int, optional): Seed for random number generation. Using a seed ensures same initialization across runs. Defaults to None.
        """

        self.n_clusters = n_clusters
        self.m = m
        self.max_iter = max_iter
        self.tolerance = tolerance
        self.random_state = random_state
        self.centroids = None  # Cluster centroids
        self.init_u = None  # Initial membership matrix
        self.U = init  # Membership matrix

    def fit(self, data):
        """
        Fits the Fuzzy C-Means model to the data.

        Args:
            data (numpy.ndarray): The input data.
        """

        # Set the random seed for reproducibility
        rng = np.random.default_rng(self.random_state)
        if self.U is None:
            self.U = rng.random((data.shape[0], self.n_clusters))
            self.U /= np.sum(self.U, axis=1)[:, np.newaxis]
            self.init_u = self.U.copy()
        self.init_u = self.U.copy()

        # Lists to store centroids and U values at each iteration
        self.centroid_history = []
        self.u_history = []

        for _ in range(self.max_iter):
            self.centroids = self._calculate_centroids(data)
            new_u = self._calculate_membership(data)

            # Store the centroids and U values
            self.centroid_history.append(self.centroids.copy())
            self.u_history.append(new_u.copy())

            if np.linalg.norm(new_u - self.U) <= self.tolerance:
                break

            self.U = new_u

    def get_centroid_history(self):
        """
        Returns the history of centroids across iterations.

        Returns:
            list: A list of numpy arrays, where each array represents centroids at an iteration.
        """
        return self.centroid_history

    def get_u_history(self):
        """
        Returns the history of membership matrices (U values) across iterations.

        Returns:
            list: A list of numpy arrays, where each array represents the membership matrix at an iteration.
        """
        return self.u_history

    def get_initial_u(self):
        """
        Returns the initial membership matrix.

        Returns:
            numpy.ndarray: The initial membership matrix (U).
        """
        return self.init_u

    def predict(self, data):
        """
        Predicts cluster assignments for new data points.

        Args:
            data (numpy.ndarray): The new data.

        Returns:
            numpy.ndarray: Cluster labels for each data point.
        """

        if self.centroids is None:
            raise ValueError("FCM model not fitted. Call fit() first.")
        return np.argmax(self._calculate_membership(data), axis=1)

    def _calculate_centroids(self, data):
        """
        Calculates cluster centroids based on current membership degrees.

        Args:
            data (numpy.ndarray): The input data.

        Returns:
            numpy.ndarray: Updated cluster centroids.
        """

        weighted_sum = np.dot((self.U**self.m).T, data)
        membership_sums = np.sum(self.U**self.m, axis=0)
        return weighted_sum / membership_sums[:, np.newaxis]

    def _calculate_membership(self, data):
        """
        Calculates membership degrees of data points to each cluster.

        Args:
            data (numpy.ndarray): The input data.

        Returns:
            numpy.ndarray: The membership matrix.
        """

        distances = np.linalg.norm(data[:, np.newaxis] - self.centroids, axis=2)
        distances[distances == 0] = np.finfo(float).eps

        inv_distances = 1 / (distances ** (2 / (self.m - 1)))
        return inv_distances / inv_distances.sum(axis=1)[:, np.newaxis]


if __name__ == "__main__":
    # Load the data
    raw_data = pd.read_excel(r"D:\Code\py_code\Fuzzy-Logic\uts\data-facial-wash.xlsx")
    raw_data = raw_data.drop(["Merk_Produk"], axis=1)
    data = raw_data.to_numpy()

    # Set hyperparameters
    n_clusters = 4
    max_iter = 1000
    m = 2
    error = 0.005
    initial_u = [
        [0.16989996, 0.36670751, 0.35030788, 0.11308465],
        [0.50992314, 0.163382, 0.10658273, 0.22011213],
        [0.46015959, 0.06140045, 0.00347142, 0.47496855],
        [0.25724951, 0.29402174, 0.35041189, 0.09831685],
        [0.1130563, 0.31894914, 0.51221235, 0.0557822],
        [0.12029269, 0.09410784, 0.56216226, 0.22343721],
        [0.03909374, 0.33328366, 0.51911104, 0.10851156],
        [0.45485111, 0.01805829, 0.03888273, 0.48820787],
        [0.2245462, 0.33967616, 0.13390469, 0.30187295],
        [0.41259956, 0.15079317, 0.06751783, 0.36908944],
        [0.00851418, 0.27403329, 0.35699791, 0.36045461],
        [0.35808648, 0.11508237, 0.23011894, 0.29671222],
        [0.44516155, 0.2781144, 0.17695283, 0.09977122],
        [0.12380086, 0.31875051, 0.03705666, 0.52039197],
        [0.14940376, 0.15189306, 0.25553106, 0.44317212],
        [0.08024304, 0.42421214, 0.14227403, 0.35327078],
        [0.11247101, 0.28654789, 0.26971779, 0.33126332],
        [0.21685796, 0.38825217, 0.2634735, 0.13141637],
        [0.18585978, 0.38503145, 0.38175499, 0.04735377],
        [0.18324605, 0.37620827, 0.29712521, 0.14342046],
        [0.29409936, 0.44311734, 0.05748537, 0.20529792],
        [0.07929185, 0.05030138, 0.40542643, 0.46498034],
        [0.1384806, 0.09289858, 0.36062263, 0.40799819],
        [0.37390788, 0.04615885, 0.57283795, 0.00709533],
        [0.22105895, 0.15768891, 0.37369088, 0.24756126],
        [0.37657239, 0.18641062, 0.23682562, 0.20019138],
        [0.16422385, 0.22317394, 0.42992725, 0.18267496],
        [0.27202726, 0.4383977, 0.22616691, 0.06340814],
        [0.45146592, 0.27187375, 0.01937135, 0.25728899],
        [0.03370402, 0.20384367, 0.0782851, 0.68416721],
        [0.40371834, 0.36062582, 0.02088494, 0.21477089],
        [0.11626782, 0.09608583, 0.4339213, 0.35372505],
        [0.03451702, 0.4256537, 0.16680041, 0.37302886],
        [0.50056303, 0.0393275, 0.26828493, 0.19182454],
        [0.25200037, 0.25754725, 0.23684704, 0.25360534],
    ]
    initial_u = np.array(initial_u)

    # Initialize and fit the FCM model
    fcm = FuzzyCMeans(
        n_clusters=n_clusters, m=m, max_iter=max_iter, tolerance=error, init=initial_u
    )

    fcm.fit(data)
    initial_u = fcm.get_initial_u()
    print(initial_u)

    # Predict cluster labels
    labels = fcm.predict(data)
    print(labels)
