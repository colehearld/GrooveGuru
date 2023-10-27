package API;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

public class RetrieveProfileData {
    public static void GetData() {
        try {
            String accessToken = SpotifyAPIClient.GetToken(SpotifyAPIClient.GetAuthorizationCode(), "AQA4QZTDTX3tTS1QzDqKEQTDZDRlGBihNFkpNYsbgQvfw6EtiTu8dP2vyc6iFL3RKwYp5V5-btBXjVMjoiouv7cUoS-8XcyKhfKYmq8L2oKNbaQOUhLWLe1hvsqL-Mc0s6A");

            String apiUrl = "https://api.spotify.com/v1/me/playlists"; //Just for testing

            URL url = new URL(apiUrl);

            HttpURLConnection connection = (HttpURLConnection) url.openConnection();

            connection.setRequestMethod("GET");

            connection.setRequestProperty("Authorization", "Bearer " + accessToken);

            int responseCode = connection.getResponseCode();

            if (responseCode == HttpURLConnection.HTTP_OK) {
                BufferedReader in = new BufferedReader(new InputStreamReader(connection.getInputStream()));
                String inputLine;
                StringBuilder response = new StringBuilder();

                while ((inputLine = in.readLine()) != null) {
                    response.append(inputLine);
                }
                in.close();

                String responseBody = response.toString();
                System.out.println("API Response: " + responseBody);
            } else {
                System.out.println("API Request failed with response code: " + responseCode);
            }

            connection.disconnect();

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}

