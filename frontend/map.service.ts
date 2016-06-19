import { Injectable } from "@angular/core";

import { MAPOBJECTS } from "./mock-mapObjects";

@Injectable()
export class MapService {
    getMapObjects() {
        return Promise.resolve(MAPOBJECTS);
    }
}
