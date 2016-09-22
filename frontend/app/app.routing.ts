import { ModuleWithProviders } from "@angular/core";
import { Routes, RouterModule } from "@angular/router";

import { MapComponent } from "./map";
import { ContactComponent } from "./contact";
import { ImprintComponent } from "./imprint";
import { AboutComponent } from "./about";

const appRoutes: Routes = [
    {
        path: "map",
        component: MapComponent,
    },
    {
        path: "contact",
        component: ContactComponent,
    },
    {
        path: "imprint",
        component: ImprintComponent,
    },
    {
        path: "about",
        component: AboutComponent,
    },
];

export const RoutingModule: ModuleWithProviders = RouterModule.forRoot(appRoutes);
