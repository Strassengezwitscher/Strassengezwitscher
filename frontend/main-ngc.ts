// The browser platform without a compiler
import { platformBrowser } from "@angular/platform-browser";
import { enableProdMode } from "@angular/core";

// The app module factory produced by the static offline compiler
import { AppModuleNgFactory } from "./app/app.module.ngfactory";

enableProdMode();
// Launch with the app module factory.
platformBrowser().bootstrapModuleFactory(AppModuleNgFactory);
