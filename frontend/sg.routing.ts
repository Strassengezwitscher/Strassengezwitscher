import { Routes, RouterModule } from "@angular/router";

import { MapComponent } from "./map.component";
import { ContactComponent } from "./contact.component";

const appRoutes: Routes = [
    {
        path: "",
        component: MapComponent,
    },
    {
        path: "contact",
        component: ContactComponent,
    },
];

export const routing = RouterModule.forRoot(appRoutes);
