import { Routes, RouterModule } from "@angular/router";

import { MapComponent } from "./map.component";
import { ContactComponent } from "./contact.component";
import { ContactSuccessComponent } from "./contactSuccess.component";

const appRoutes: Routes = [
    {
        path: "",
        component: MapComponent,
    },
    {
        path: "contact",
        component: ContactComponent,
    },
    {
        path: "contact/success",
        component: ContactSuccessComponent,
    },
];

export const RoutingModule = RouterModule.forRoot(appRoutes);
