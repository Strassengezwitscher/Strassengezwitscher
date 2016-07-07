import { StrassengezwitscherComponent } from '../sg.component';

describe('StrassengezwitscherComponent', () => {

  beforeEach(function() {
    this.app = new StrassengezwitscherComponent();
  });

  it('should have hello property', function() {
    expect(this.app.somevar).toBe('Hello');
  });

});
