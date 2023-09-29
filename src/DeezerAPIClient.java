import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

public class DeezerAPIClient {

    //TODO: Add OAuth to successfully access deezer API
    public void APIConnect(String app_id, String app_secret, String my_url) {
        String apiUrl = "https://api.deezer.com/search?q=artist:\"Ed Sheeran\"";

        try {
            URL url = new URL(apiUrl);

            HttpURLConnection connection = (HttpURLConnection) url.openConnection();

            connection.setRequestMethod("GET");

            int responseCode = connection.getResponseCode();

            if (responseCode == HttpURLConnection.HTTP_OK) {
                // Read and print the response content
                BufferedReader in = new BufferedReader(new InputStreamReader(connection.getInputStream()));
                String inputLine;
                StringBuilder response = new StringBuilder();

                while ((inputLine = in.readLine()) != null) {
                    response.append(inputLine);
                }

                in.close();

                // Print the response content
                System.out.println(response.toString());
            } else {
                System.err.println("HTTP Request Failed with status code: " + responseCode);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}



