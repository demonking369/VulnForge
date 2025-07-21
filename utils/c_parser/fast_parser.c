#include <stdio.h>
#include <stdlib.h>
#include "cJSON.h"

// This function will be exported to be used by Python
// It takes a raw JSON string and returns a simplified summary
char* parse_nuclei_output(const char* json_string) {
    cJSON *root = cJSON_Parse(json_string);
    if (root == NULL) {
        return "{\"error\": \"Invalid JSON\"}";
    }

    int critical_count = 0;
    cJSON *item;
    cJSON_ArrayForEach(item, root) {
        cJSON *info = cJSON_GetObjectItem(item, "info");
        if (info) {
            cJSON *severity = cJSON_GetObjectItem(info, "severity");
            if (cJSON_IsString(severity) && (strcmp(severity->valuestring, "critical") == 0)) {
                critical_count++;
            }
        }
    }

    cJSON_Delete(root);

    // Create a simple summary string to return
    char* summary = malloc(128);
    sprintf(summary, "{\"critical_findings\": %d}", critical_count);
    return summary;
} 