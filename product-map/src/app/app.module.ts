import {BrowserModule} from  '@angular/platform-browser'
import { NgModule, ChangeDetectorRef } from '@angular/core';
import { AppComponent } from './app.component';
import { MapComponent } from './map/map.component';
import { ProductComponent } from './product/product.component';
import { PrecisionPipe, KeysPipe} from './precision.pipe';
import { HttpClientModule } from '@angular/common/http';

import { DataService } from "./services/data.service";
import { ColorbarService} from "./services/colorbar.service";
import { ProductService} from "./services/product.service";
import { PrintService} from "./services/print.service";

import { SidebarComponent } from './sidebar/sidebar.component';
import { GalleryComponent } from './gallery/gallery.component';
import { TimelineComponent } from './timeline/timeline.component';
import { VectorProductComponent } from './vector-product/vector-product.component';
import { SearchbarComponent } from './searchbar/searchbar.component';
import { RegionComponent } from './region/region.component';
import { ColorbarComponent } from './colorbar/colorbar.component';
import { OptionsComponent } from './options/options.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

import { StorageServiceModule } from 'angular-webstorage-service';
import { ProductsComponent } from './admin/products/products.component';
import { ImageComponent } from './gallery/image/image.component';

import { ColorPickerModule } from 'ngx-color-picker';
import { LayerComponent } from './options/layer/layer.component';
import { ColorbarEditorComponent } from './colorbar/colorbar-editor/colorbar-editor.component';


@NgModule({
  declarations: [
    AppComponent,
    MapComponent,
    ProductComponent,
    PrecisionPipe,
    KeysPipe,
    SidebarComponent,
    GalleryComponent,
    TimelineComponent,
    VectorProductComponent,
    SearchbarComponent,
    RegionComponent,
    ColorbarComponent,
    OptionsComponent,
    ProductsComponent,
    ImageComponent,
    LayerComponent,
    ColorbarEditorComponent
  ],
  imports: [
    ColorPickerModule,
    BrowserModule,
    FormsModule,
    StorageServiceModule, 
    HttpClientModule,
    ReactiveFormsModule
  ],
  providers: [DataService, ColorbarService, PrintService, ProductService, ChangeDetectorRef],
  bootstrap: [AppComponent]
})
export class AppModule { }
