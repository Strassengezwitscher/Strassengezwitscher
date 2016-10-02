import { NgModule, CUSTOM_ELEMENTS_SCHEMA } from "@angular/core";
import { MaterialModule } from "@angular/material";

import { AboutComponent } from "./about.component";
import { routing } from "./about.routing";

@NgModule({
  imports: [MaterialModule, routing],
  declarations: [AboutComponent],
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
})
export class AboutModule {}
