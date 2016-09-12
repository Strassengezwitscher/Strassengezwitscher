import { platformBrowserDynamic } from "@angular/platform-browser-dynamic";

import { Config } from "./config/config";
import { AppModule } from "./app/app.module";

let config = new Config();
config.configure();
platformBrowserDynamic().bootstrapModule(AppModule);
