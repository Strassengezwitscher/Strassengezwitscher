/// <reference path="../typings/browser.d.ts" />

import { bootstrap } from "@angular/platform-browser-dynamic";
import { ROUTER_PROVIDERS } from "@angular/router";
import { HTTP_PROVIDERS } from "@angular/http";

import { StrassengezwitscherComponent } from "./sg.component";

bootstrap(StrassengezwitscherComponent, [ROUTER_PROVIDERS, HTTP_PROVIDERS]);
