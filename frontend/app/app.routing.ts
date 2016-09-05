import { ModuleWithProviders } from "@angular/core";
import { Routes, RouterModule } from "@angular/router";

import { MapComponent } from "./map";
import { ContactComponent } from "./contact";

const appRoutes: Routes = [
    {
        path: "map",
        component: MapComponent,
    },
    {
        path: "map/contact",
        component: ContactComponent,
    },
];

export const RoutingModule: ModuleWithProviders = RouterModule.forRoot(appRoutes);
