import { Component, Output, EventEmitter } from "@angular/core";

import { MapService } from "../map.service";
import { MapObjectType, MapObjectTypeNaming } from "../mapObject.model";

// ADD DICTIONARY for MAPPING of Object Type

@Component({
    moduleId: module.id,
    selector: "cg-map-object-creation",
    templateUrl: "mapObjectCreation.component.html",
    styleUrls: ["mapObjectCreation.component.css"],
})
export class MapObjectCreationComponent {
    @Output() public onError = new EventEmitter<string>();
    public selectedMapObjectType: MapObjectType;
    public mapObjectType = MapObjectType;
    public mapObjectTypes = MapObjectTypeNaming;
    public currentTime = new Date();
    constructor(private mapService: MapService) {}

    public send(moc) {
        console.log(this.selectedMapObjectType);
        console.log(moc);
    }

}
