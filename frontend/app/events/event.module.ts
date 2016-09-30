import { NgModule, CUSTOM_ELEMENTS_SCHEMA } from "@angular/core";
import { BrowserModule } from "@angular/platform-browser";

import { EventComponent } from "./event/event.component";
import { EventDetailComponent } from "./eventDetail/eventDetail.component";
import { EventService } from "./shared/event.service";
import { routing } from "./event.routing";

@NgModule({
  imports: [BrowserModule, routing],
  declarations: [EventComponent, EventDetailComponent],
  exports: [EventComponent, EventDetailComponent],
  providers: [EventService],
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
})
export class EventModule {}
