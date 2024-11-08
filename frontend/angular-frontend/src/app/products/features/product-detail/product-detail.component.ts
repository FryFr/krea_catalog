import { Component, effect, inject, input } from '@angular/core';
import { ProductDetailSateService } from '../../data-access/proudct-detail-state.service';
import { CurrencyPipe } from '@angular/common';
import { CartStateService } from '../../../shared/data-access/cart-state.service';
import { PdfViewerModule } from 'ng2-pdf-viewer';


@Component({
  selector: 'app-product-detail',
  standalone: true,
  imports: [CurrencyPipe, PdfViewerModule],
  templateUrl: './product-detail.component.html',
  providers: [ProductDetailSateService],
})
export default class ProductDetailComponent {
  src = 'https://fryfr.github.io/calculadora_electronica/lib/15.1%20DRYWALL%20Y%20ACCESORIOS.pdf';
  productDetailState = inject(ProductDetailSateService).state;
  cartState = inject(CartStateService).state;

  id = input.required<string>();

  constructor() {
    effect(() => {
      this.productDetailState.getById(this.id());
    });
  }

  addToCart() {
    this.cartState.add({
      product: this.productDetailState.product()!,
      quantity: 1,
    });
  }
}
