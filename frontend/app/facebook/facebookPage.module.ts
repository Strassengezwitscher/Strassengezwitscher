import { NgModule, CUSTOM_ELEMENTS_SCHEMA } from "@angular/core";
import { BrowserModule } from "@angular/platform-browser";
import { MaterialModule } from "@angular/material";

import { FacebookPageComponent } from "./facebookPage.component";
import { FacebookPageService } from "./facebookPage.service";

@NgModule({
  imports: [BrowserModule, MaterialModule],
  declarations: [FacebookPageComponent],
  exports: [FacebookPageComponent],
  providers: [FacebookPageService],
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
})
export class FacebookPageModule {}
