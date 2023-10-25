import com.google.gson.Gson;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.Scanner;

public class SpotifyAPIClient {
    static final String CLIENT_ID = "ad5775b4672c46ba9c118ace167e62ba";
    static final String CLIENT_SECRET = "fd6631ea69f9425985187b2af81e4f79";
    static final String REDIRECT_URI = "http://localhost:8888/callback"; // Update with callback URL
    static final String AUTH_URL = "https://accounts.spotify.com/authorize";
    static final String TOKEN_URL = "https://accounts.spotify.com/api/token";
    static final String SCOPE = "user-read-private%20user-read-email";

    public static String GetAuthorizationCode() {
        // Step 1: Redirect the user to the authorization page
        String authUrl = AUTH_URL +
                "?client_id=" + CLIENT_ID +
                "&response_type=code" +
                "&redirect_uri=" + REDIRECT_URI +
                "&scope=" + SCOPE;

        System.out.println("Open the following URL in your browser to log in and grant permissions:");
        System.out.println(authUrl);

        // After the user grants permissions, they will be redirected back to the callback URL
        System.out.print("Enter the authorization code from the URL: ");
        Scanner scanner = new Scanner(System.in);
        String authorizationCode = scanner.nextLine();

        return authorizationCode;
    }

    public static String GetToken(String authorizationCode) {

        try {
            URL tokenUrl = new URL(TOKEN_URL);
            HttpURLConnection tokenConn = (HttpURLConnection) tokenUrl.openConnection();
            tokenConn.setRequestMethod("POST");
            tokenConn.setDoOutput(true);

            String postData = "grant_type=authorization_code" +
                    "&code=" + authorizationCode +
                    "&redirect_uri=" + REDIRECT_URI +
                    "&client_id=" + CLIENT_ID +
                    "&client_secret=" + CLIENT_SECRET;

            tokenConn.getOutputStream().write(postData.getBytes("UTF-8"));

            if (tokenConn.getResponseCode() != 200) {
                throw new RuntimeException("Failed to retrieve access token. HTTP error code: " + tokenConn.getResponseCode());
            }

            BufferedReader tokenReader = new BufferedReader(new InputStreamReader(tokenConn.getInputStream()));
            String tokenResponse;
            StringBuilder tokenResponseBuilder = new StringBuilder();

            while ((tokenResponse = tokenReader.readLine()) != null) {
                tokenResponseBuilder.append(tokenResponse);
            }

            // Parse and handle the JSON response to get the access token

            // use Gson to parse tokenResponse and get access token
            Gson gson = new Gson();
            AccessToken user_access_token = gson.fromJson(tokenResponseBuilder.toString(), AccessToken.class);

            System.out.println("Access Token: " + user_access_token.getAccess_token());

            tokenConn.disconnect();
        } catch (MalformedURLException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
        return null;
    }

    private static String parseAccessToken(String json) {
        // Parse the JSON response to extract the access token
        // This parsing logic depends on the JSON structure of the token response
        // We may want to use a JSON parsing library like Jackson or Gson for production code
        // Currently, we assume a simple JSON structure like {"access_token": "TOKEN_VALUE"}
        int startIndex = json.indexOf("\"access_token\":\"") + 15;
        int endIndex = json.indexOf("\"", startIndex);
        return json.substring(startIndex, endIndex);
    }
}