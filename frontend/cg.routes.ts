import { provideRouter, RouterConfig } from "@angular/router";

import { MapComponent } from "./map.component";
import { ContactComponent } from "./contact.component";

export const routes: RouterConfig = [
    { path: "", component: MapComponent },
    { path: "contact", component: ContactComponent },
];

export const APP_ROUTER_PROVIDERS = [
  provideRouter(routes),
];
