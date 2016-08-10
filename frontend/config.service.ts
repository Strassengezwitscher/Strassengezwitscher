import { Injectable }       from "@angular/core";

@Injectable()
export class ConfigurationService {
    private config;
    // Temporary workaround find good way to handle json file in build version, which is loaded using http.
    constructor() {
        this.config = {"data-sitekey": "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI"};
    }

    public getConfigEntry(key) {
        return this.config[key];
    }
}
