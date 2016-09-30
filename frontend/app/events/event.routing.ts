import { ModuleWithProviders } from "@angular/core";
import { RouterModule } from "@angular/router";

import { EventDetailComponent } from "./eventDetail/eventDetail.component";

export const routing: ModuleWithProviders = RouterModule.forChild([
    { path: "events/:id", component: EventDetailComponent},
]);
