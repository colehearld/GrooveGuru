import com.google.gson.Gson;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;

public class SpotifyAPIClient {
    static final String CLIENT_ID = "a7a02e00f9664daaa47b8517d1d8bbcb";
    static final String CLIENT_SECRET = "83b3b5cbe9e54e7a9c19f03dba86039d";
    static final String REDIRECT_URI = "https://localhost:8087/callback";
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

        //System.out.println("Open the following URL in your browser to log in and grant permissions:");
        //System.out.println(authUrl);

        //After the user grants permissions, they will be redirected back to the callback URL
        //System.out.print("Enter the authorization code from the URL: ");
        //Scanner scanner = new Scanner(System.in);
        //String authorizationCode = scanner.nextLine();

        String authorizationCode = "AQA4QZTDTX3tTS1QzDqKEQTDZDRlGBihNFkpNYsbgQvfw6EtiTu8dP2vyc6iFL3RKwYp5V5";

        return authorizationCode;
    }

    public static String GetToken(String authorizationCode, String refreshToken) {
        if (refreshToken != null && !refreshToken.isEmpty()) {
            // If a refresh token is available, try to refresh the access token
            return refreshTokenFlow(refreshToken);
        } else {
            // If no refresh token is available, use the authorization code
            return authorizationCodeFlow(authorizationCode);
        }
    }

    private static String refreshTokenFlow(String refreshToken) {
        AccessToken userAccessToken = null;
        try {
            URL tokenUrl = new URL(TOKEN_URL);
            HttpURLConnection tokenConn = (HttpURLConnection) tokenUrl.openConnection();
            tokenConn.setRequestMethod("POST");
            tokenConn.setDoOutput(true);

            String postData = "grant_type=refresh_token" +
                    "&refresh_token=" + refreshToken +
                    "&client_id=" + CLIENT_ID +
                    "&client_secret=" + CLIENT_SECRET;

            tokenConn.getOutputStream().write(postData.getBytes("UTF-8"));

            if (tokenConn.getResponseCode() != 200) {
                throw new RuntimeException("Failed to refresh access token. HTTP error code: " + tokenConn.getResponseCode());
            }

            BufferedReader tokenReader = new BufferedReader(new InputStreamReader(tokenConn.getInputStream()));
            String tokenResponse;
            StringBuilder tokenResponseBuilder = new StringBuilder();

            while ((tokenResponse = tokenReader.readLine()) != null) {
                tokenResponseBuilder.append(tokenResponse);
            }

            // Parse and handle the JSON response to get the access token and optionally a new refresh token
            Gson gson = new Gson();
            userAccessToken = gson.fromJson(tokenResponseBuilder.toString(), AccessToken.class);

            //System.out.println("Access Token: " + userAccessToken.getAccess_token());
            //System.out.println("Refresh Token: " + userAccessToken.getRefresh_token());

            tokenConn.disconnect();
        } catch (MalformedURLException e) {
            e.printStackTrace();
        } catch (Exception e) {
            e.printStackTrace();
        }

        return userAccessToken.getAccess_token();
    }

    private static String authorizationCodeFlow(String authorizationCode) {
        AccessToken userAccessToken = null;
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

            // use Gson to parse tokenResponse and get access token and refresh token
            Gson gson = new Gson();
            userAccessToken = gson.fromJson(tokenResponseBuilder.toString(), AccessToken.class);

            //System.out.println("Access Token: " + userAccessToken.getAccess_token());
            //System.out.println("Refresh Token: " + userAccessToken.getRefresh_token());

            tokenConn.disconnect();
        } catch (MalformedURLException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
        return "Replace with your code to get access token using the authorization code";
    }
}

