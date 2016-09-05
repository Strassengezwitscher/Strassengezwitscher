import { Routes, RouterModule } from "@angular/router";

import { MapComponent } from "../map/map.component";
import { ContactComponent } from "../contact/contact.component";

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
