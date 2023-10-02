import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

public class DeezerAPIClient {
    public static void main(String[] args) {
        String appId = "YOUR_APP_ID";
        String appSecret = "YOUR_APP_SECRET";
        String myUrl = "YOUR_CALLBACK_URL";

        // Start a session (not required in Java, as sessions are typically managed on the server-side)
        String state = UUID.randomUUID().toString(); // CSRF protection

        String code = ""; // The code you receive from the Deezer OAuth callback should be set here.

        if (code.isEmpty()) {
            // Redirect to Deezer's OAuth dialog
            String dialogUrl = "https://connect.deezer.com/oauth/auth.php?app_id=" + appId
                    + "&redirect_uri=" + myUrl + "&perms=email,offline_access" + "&state=" + state;

            System.out.println("Redirecting to: " + dialogUrl);
            // Implement redirection logic as needed in your application
        }

        if (state.equals("received_state_from_deezer")) { // Replace with the actual received state
            // Exchange the code for an access token
            String tokenUrl = "https://connect.deezer.com/oauth/access_token.php?app_id="
                    + appId + "&secret=" + appSecret + "&code=" + code;

            try {
                String response = sendGET(tokenUrl);

                // Parse the response to get the access token
                Map<String, String> params = parseQueryString(response);

                String accessToken = params.get("access_token");

                // Use the access token to make API requests
                String apiUrl = "https://api.deezer.com/user/me?access_token=" + accessToken;
                String apiResponse = sendGET(apiUrl);

                // Handle the API response (e.g., parse JSON)
                System.out.println("API Response: " + apiResponse);
            } catch (Exception e) {
                e.printStackTrace();
                System.out.println("Error: " + e.getMessage());
            }
        } else {
            System.out.println("The state does not match. You may be a victim of CSRF.");
        }
    }

    // Helper method to send a GET request and receive a response
    private static String sendGET(String url) throws Exception {
        URL obj = new URL(url);
        HttpURLConnection connection = (HttpURLConnection) obj.openConnection();

        connection.setRequestMethod("GET");

        int responseCode = connection.getResponseCode();

        if (responseCode == HttpURLConnection.HTTP_OK) {
            BufferedReader in = new BufferedReader(new InputStreamReader(connection.getInputStream()));
            StringBuilder response = new StringBuilder();
            String inputLine;

            while ((inputLine = in.readLine()) != null) {
                response.append(inputLine);
            }

            in.close();

            return response.toString();
        } else {
            throw new Exception("HTTP GET request failed with response code: " + responseCode);
        }
    }

    // Helper method to parse query string parameters
    private static Map<String, String> parseQueryString(String queryString) {
        Map<String, String> params = new HashMap<>();

        String[] keyValuePairs = queryString.split("&");

        for (String pair : keyValuePairs) {
            String[] parts = pair.split("=");
            if (parts.length == 2) {
                String key = parts[0];
                String value = parts[1];
                params.put(key, value);
            }
        }

        return params;
    }
}




