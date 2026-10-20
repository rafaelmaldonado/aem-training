describe('Published TrainingMessage', () => {
  it('shows the authored title to a visitor', () => {
    cy.env(['publishPageUrl', 'expectedTitle']).then(({ publishPageUrl, expectedTitle }) => {
      expect(Boolean(publishPageUrl), 'publishPageUrl supplied').to.be.true
      expect(Boolean(expectedTitle), 'expectedTitle supplied').to.be.true

      cy.visit(publishPageUrl)
      cy.get('[data-cy="training-message"] h2').should('be.visible').and('have.text', expectedTitle)
    })
  })
})
