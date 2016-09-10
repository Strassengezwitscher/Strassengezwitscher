// tslint:disable-next-line:no-reference
/// <reference path="../typings/index.d.ts" />

// The browser platform without a compiler
import { platformBrowser } from "@angular/platform-browser";

// The app module factory produced by the static offline compiler
import { AppModuleNgFactory } from "./app/app.module.ngfactory";

// Launch with the app module factory.
platformBrowser().bootstrapModuleFactory(AppModuleNgFactory);
