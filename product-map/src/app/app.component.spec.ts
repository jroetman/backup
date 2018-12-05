import { TestBed, async } from '@angular/core/testing';
import { AppComponent } from './app.component';
import { MapComponent } from './map/map.component';
import { ProductComponent } from './product/product.component';
import { DataService } from "./services/data.service";
import { SidebarComponent } from './sidebar/sidebar.component';
import { GalleryComponent } from './gallery/gallery.component';
import { TimelineComponent } from './timeline/timeline.component';
import { PrecisionPipe, KeysPipe} from './precision.pipe';

describe('AppComponent', () => {
  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [
        AppComponent, MapComponent, ProductComponent, SidebarComponent, GalleryComponent, TimelineComponent,
        PrecisionPipe,
        KeysPipe,
      ],
      providers: [DataService]
    }).compileComponents();
  }));
  it('should create the app', async(() => {
    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.debugElement.componentInstance;
    expect(app).toBeTruthy();
  }));
});
