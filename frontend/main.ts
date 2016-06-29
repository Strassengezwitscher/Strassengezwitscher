// tslint:disable-next-line:no-reference
/// <reference path="../typings/browser.d.ts" />

import { bootstrap } from "@angular/platform-browser-dynamic";
import { HTTP_PROVIDERS } from "@angular/http";

import { StrassengezwitscherComponent } from "./sg.component";
import { APP_ROUTER_PROVIDERS } from "./sg.routes";

bootstrap(StrassengezwitscherComponent, [
    APP_ROUTER_PROVIDERS,
    HTTP_PROVIDERS,
])
.catch(err => console.error(err));
