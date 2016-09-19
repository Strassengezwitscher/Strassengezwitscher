import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Params } from '@angular/router';

import { Event, EventService } from "./";

@Component({
    moduleId: module.id,
    selector: "cg-event-detailPage",
    templateUrl: "eventDetail.component.html",
    providers: [EventService],
})

export class EventDetailComponent {
    private activeEvent: Event;
    constructor(private eventService: EventService, private route: ActivatedRoute) {
        this.activeEvent = new Event();
    }

    private getEventDetails(id: number) {
        this.eventService.getEvent(id)
                        .subscribe(
                            event => this.setActiveEvent(event),
                            error => console.log(error)
                        );
    }

    ngOnInit(): void {
        this.route.params.forEach((params: Params) => {
          let id = +params['id'];
          this.getEventDetails(id);
        });
    }

    private setActiveEvent(event: Event) {
        this.activeEvent = event;
    }
}
