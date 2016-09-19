import { ModuleWithProviders } from "@angular/core";
import { Routes, RouterModule } from "@angular/router";

import { MapComponent } from "./map";
import { ContactComponent } from "./contact";
import { ImprintComponent } from "./imprint";
import { AboutComponent } from "./about";
import { EventDetailComponent } from "./events";

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
    {
        path: "event/:id",
        component: EventDetailComponent,
    },
];

export const RoutingModule: ModuleWithProviders = RouterModule.forRoot(appRoutes);
