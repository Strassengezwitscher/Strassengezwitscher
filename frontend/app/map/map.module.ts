import { NgModule, CUSTOM_ELEMENTS_SCHEMA } from "@angular/core";
import { BrowserModule } from "@angular/platform-browser";
import { FormsModule } from "@angular/forms";
import { MaterialModule } from "@angular/material";

import { MapComponent } from "./map.component";
import { MapObjectCreationComponent } from "./mapObjectCreation/mapObjectCreation.component";
import { MapService } from "./map.service";
import { routing } from "./map.routing";
import { EventModule } from "../events/event.module";
import { FacebookPageModule } from "../facebook/facebookPage.module";

@NgModule({
  imports: [MaterialModule, BrowserModule, FormsModule, routing, EventModule, FacebookPageModule],
  declarations: [MapComponent, MapObjectCreationComponent],
  exports: [MapComponent, MapObjectCreationComponent],
  providers: [MapService],
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
})
export class MapModule {}
