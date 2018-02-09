import { NgModule, CUSTOM_ELEMENTS_SCHEMA } from "@angular/core";
import { MaterialModule } from "@angular/material";

import { DonateComponent } from "./donate.component";
import { routing } from "./donate.routing";

@NgModule({
  imports: [MaterialModule, routing],
  declarations: [DonateComponent],
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
})
export class DonateModule {}
