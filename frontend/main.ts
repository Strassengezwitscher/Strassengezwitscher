// tslint:disable-next-line:no-reference
/// <reference path="../typings/index.d.ts" />

import { platformBrowserDynamic } from "@angular/platform-browser-dynamic";

import { Config } from "./config/config";
import { CrowdgezwitscherModule } from "./cg/cg.module";

let config = new Config();
config.configure();
platformBrowserDynamic().bootstrapModule(CrowdgezwitscherModule);
