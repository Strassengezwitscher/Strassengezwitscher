import { ModuleWithProviders } from "@angular/core";
import { RouterModule } from "@angular/router";

import { MapComponent } from "./map.component";

export const routing: ModuleWithProviders = RouterModule.forChild([
  { path: "map", component: MapComponent},
]);
