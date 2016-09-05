import { Routes, RouterModule } from "@angular/router";

import { MapComponent } from "../map/index";
import { ContactComponent } from "../contact/index";

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

export const RoutingModule = RouterModule.forRoot(appRoutes);
