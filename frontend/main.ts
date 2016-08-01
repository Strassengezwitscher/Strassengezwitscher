// tslint:disable-next-line:no-reference
/// <reference path="../typings/index.d.ts" />

import { bootstrap } from "@angular/platform-browser-dynamic";
import { HTTP_PROVIDERS } from "@angular/http";
import { disableDeprecatedForms, provideForms } from "@angular/forms";

import { StrassengezwitscherComponent } from "./sg.component";
import { APP_ROUTER_PROVIDERS } from "./sg.routes";

bootstrap(StrassengezwitscherComponent, [
    APP_ROUTER_PROVIDERS,
    HTTP_PROVIDERS,
    disableDeprecatedForms(),
    provideForms(),
])
.catch(err => console.error(err));
