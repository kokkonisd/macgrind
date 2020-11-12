#include <stdio.h>
#include <curl/curl.h>

int main (int argc, char * argv[])
{
    printf("Hello, World!\n");

    CURL * curl = curl_easy_init();

    if (curl) {
        CURLcode res;
          curl_easy_setopt(curl, CURLOPT_URL, "https://kokkonisd.github.io");
          res = curl_easy_perform(curl);
          curl_easy_cleanup(curl);
    }

    return 0;
}
