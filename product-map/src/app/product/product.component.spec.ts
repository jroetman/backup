import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import {DataService} from '../services/data.service'
import { ProductComponent } from './product.component';
import { PrecisionPipe, KeysPipe} from '../precision.pipe';

describe('ProductComponent', () => {
  let component: ProductComponent;
  let fixture: ComponentFixture<ProductComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ProductComponent, KeysPipe ],
      providers: [DataService]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ProductComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

});
