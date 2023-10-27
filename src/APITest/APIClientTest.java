package APITest;

import API.SpotifyAPIClient;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class APIClientTest {

    @Test
    public void testGetAuthorizationCode() {
        String expectedAuthorizationCode = "AQA4QZTDTX3tTS1QzDqKEQTDZDRlGBihNFkpNYsbgQvfw6EtiTu8dP2vyc6iFL3RKwYp5V5";
        String actualAuthorizationCode = SpotifyAPIClient.GetAuthorizationCode();
        assertEquals(expectedAuthorizationCode, actualAuthorizationCode);
    }
}
