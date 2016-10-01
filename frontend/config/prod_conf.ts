import { SensitiveConfig } from "./sensitive_conf";

export class Config {
    public dataSitekey = "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI";

    constructor() {
        this.initFromSensitiveConfig(new SensitiveConfig());
    }

    private initFromSensitiveConfig(sConf: SensitiveConfig) {
        for (let key in sConf) {
            if (sConf.hasOwnProperty(key)) {
                this[key] = sConf[key];
            }
        }
    }
}
